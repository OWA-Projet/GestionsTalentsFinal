import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Postuler } from './postuler';

describe('Postuler', () => {
  let component: Postuler;
  let fixture: ComponentFixture<Postuler>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Postuler]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Postuler);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
