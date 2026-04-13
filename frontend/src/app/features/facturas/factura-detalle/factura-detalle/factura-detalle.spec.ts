import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FacturaDetalle } from './factura-detalle';

describe('FacturaDetalle', () => {
  let component: FacturaDetalle;
  let fixture: ComponentFixture<FacturaDetalle>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FacturaDetalle],
    }).compileComponents();

    fixture = TestBed.createComponent(FacturaDetalle);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
