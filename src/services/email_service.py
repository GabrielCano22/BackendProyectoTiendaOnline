"""
Servicio de notificaciones por email — La Tienda de Gerardo
"""

import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decimal import Decimal

from sqlalchemy.orm import Session
from src.entities.factura import Factura
from src.entities.usuario import Usuario

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.resend.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM", "")


def _obtener_email_cliente(factura: Factura, db: Session) -> str | None:
    """Obtiene el email del dueño de la factura."""
    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == factura.id_usuario
    ).first()
    return usuario.email if usuario else None


def _formato_moneda(valor) -> str:
    return f"${Decimal(str(valor)):,.2f}"


def _html_factura_aprobada(factura: Factura, nombre_cliente: str) -> str:
    return f"""\
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#0F1117;font-family:'Segoe UI',Arial,sans-serif;">
  <div style="max-width:600px;margin:40px auto;background:#161B25;border-radius:16px;border:1px solid #2A3347;overflow:hidden;">
    <!-- Header -->
    <div style="background:linear-gradient(135deg,#059669,#10B981);padding:32px;text-align:center;">
      <div style="width:56px;height:56px;background:rgba(255,255,255,.2);border-radius:50%;margin:0 auto 16px;display:flex;align-items:center;justify-content:center;">
        <span style="font-size:28px;">&#10003;</span>
      </div>
      <h1 style="color:#fff;margin:0;font-size:24px;">Compra Aprobada</h1>
      <p style="color:rgba(255,255,255,.8);margin:8px 0 0;font-size:14px;">Tu pago ha sido verificado exitosamente</p>
    </div>
    <!-- Body -->
    <div style="padding:32px;">
      <p style="color:#E2E8F0;font-size:16px;margin:0 0 24px;">
        Hola <strong>{nombre_cliente}</strong>,
      </p>
      <p style="color:#94A3B8;font-size:14px;line-height:1.6;margin:0 0 24px;">
        Tu factura <strong style="color:#E2E8F0;">#{str(factura.id_factura)[:8].upper()}</strong>
        ha sido <strong style="color:#10B981;">aprobada</strong> por nuestro equipo.
        Tu pedido sera procesado y enviado a la brevedad.
      </p>
      <!-- Resumen -->
      <div style="background:#1C2333;border:1px solid #2A3347;border-radius:12px;padding:20px;margin-bottom:24px;">
        <h3 style="color:#E2E8F0;margin:0 0 16px;font-size:14px;text-transform:uppercase;letter-spacing:.05em;">Resumen del pedido</h3>
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
          <span style="color:#94A3B8;font-size:14px;">Subtotal</span>
          <span style="color:#E2E8F0;font-size:14px;">{_formato_moneda(factura.total_bruto)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
          <span style="color:#4ADE80;font-size:14px;">Descuento ({factura.porcentaje_descuento}%)</span>
          <span style="color:#4ADE80;font-size:14px;">-{_formato_moneda(factura.total_descuento)}</span>
        </div>
        <div style="height:1px;background:#2A3347;margin:12px 0;"></div>
        <div style="display:flex;justify-content:space-between;">
          <span style="color:#E2E8F0;font-size:16px;font-weight:700;">Total</span>
          <span style="color:#10B981;font-size:18px;font-weight:800;">{_formato_moneda(factura.total_neto)}</span>
        </div>
      </div>
      <p style="color:#64748B;font-size:13px;margin:0;text-align:center;">
        Gracias por tu compra en <strong style="color:#94A3B8;">La Tienda de Gerardo</strong>
      </p>
    </div>
  </div>
</body>
</html>"""


def _html_factura_rechazada(factura: Factura, nombre_cliente: str) -> str:
    return f"""\
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#0F1117;font-family:'Segoe UI',Arial,sans-serif;">
  <div style="max-width:600px;margin:40px auto;background:#161B25;border-radius:16px;border:1px solid #2A3347;overflow:hidden;">
    <!-- Header -->
    <div style="background:linear-gradient(135deg,#DC2626,#B91C1C);padding:32px;text-align:center;">
      <div style="width:56px;height:56px;background:rgba(255,255,255,.2);border-radius:50%;margin:0 auto 16px;display:flex;align-items:center;justify-content:center;">
        <span style="font-size:28px;">&#10007;</span>
      </div>
      <h1 style="color:#fff;margin:0;font-size:24px;">Compra Rechazada</h1>
      <p style="color:rgba(255,255,255,.8);margin:8px 0 0;font-size:14px;">No pudimos verificar tu pago</p>
    </div>
    <!-- Body -->
    <div style="padding:32px;">
      <p style="color:#E2E8F0;font-size:16px;margin:0 0 24px;">
        Hola <strong>{nombre_cliente}</strong>,
      </p>
      <p style="color:#94A3B8;font-size:14px;line-height:1.6;margin:0 0 24px;">
        Lamentamos informarte que tu factura
        <strong style="color:#E2E8F0;">#{str(factura.id_factura)[:8].upper()}</strong>
        ha sido <strong style="color:#F87171;">rechazada</strong>.
        No fue posible comprobar el pago asociado a esta compra.
      </p>
      <div style="background:rgba(220,38,38,.08);border:1px solid rgba(220,38,38,.2);border-radius:12px;padding:16px;margin-bottom:24px;">
        <p style="color:#F87171;font-size:14px;margin:0 0 8px;font-weight:600;">Motivo del rechazo:</p>
        <p style="color:#94A3B8;font-size:14px;margin:0;line-height:1.5;">
          El pago no pudo ser comprobado o verificado por nuestro equipo.
          Los productos han sido devueltos al inventario.
        </p>
      </div>
      <!-- Resumen -->
      <div style="background:#1C2333;border:1px solid #2A3347;border-radius:12px;padding:20px;margin-bottom:24px;">
        <h3 style="color:#E2E8F0;margin:0 0 16px;font-size:14px;text-transform:uppercase;letter-spacing:.05em;">Factura anulada</h3>
        <div style="display:flex;justify-content:space-between;">
          <span style="color:#94A3B8;font-size:14px;">Total que no fue cobrado</span>
          <span style="color:#E2E8F0;font-size:16px;font-weight:700;text-decoration:line-through;">{_formato_moneda(factura.total_neto)}</span>
        </div>
      </div>
      <p style="color:#94A3B8;font-size:14px;line-height:1.6;margin:0 0 24px;">
        Si crees que esto es un error, puedes contactarnos o realizar una nueva compra.
      </p>
      <p style="color:#64748B;font-size:13px;margin:0;text-align:center;">
        <strong style="color:#94A3B8;">La Tienda de Gerardo</strong> — Soporte al cliente
      </p>
    </div>
  </div>
</body>
</html>"""


def enviar_email_estado_factura(factura: Factura, estado: str, db: Session) -> None:
    """
    Envía un email al cliente notificando el cambio de estado de su factura.
    Se ejecuta como background task para no bloquear la respuesta.
    """
    if not SMTP_USER or not SMTP_PASS:
        logger.warning("SMTP no configurado — email no enviado para factura %s", factura.id_factura)
        return

    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == factura.id_usuario
    ).first()
    if not usuario or not usuario.email:
        logger.warning("No se encontró email del cliente para factura %s", factura.id_factura)
        return

    nombre = usuario.nombre
    destino = usuario.email

    if estado == "aprobada":
        asunto = f"Compra aprobada — Factura #{str(factura.id_factura)[:8].upper()}"
        html = _html_factura_aprobada(factura, nombre)
    else:
        asunto = f"Compra rechazada — Factura #{str(factura.id_factura)[:8].upper()}"
        html = _html_factura_rechazada(factura, nombre)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = asunto
    msg["From"] = SMTP_FROM or SMTP_USER
    msg["To"] = destino
    msg.attach(MIMEText(html, "html"))

    try:
        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
        logger.info("Email enviado a %s — factura %s %s", destino, factura.id_factura, estado)
    except Exception as e:
        logger.error("Error enviando email a %s: %s", destino, str(e))
