#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tienda Online - La Tienda de Gerardo
"""

from sistema_gestion import SistemaGestion


def main():
    with SistemaGestion() as sistema:
        sistema.ejecutar()


if __name__ == "__main__":
    main()

