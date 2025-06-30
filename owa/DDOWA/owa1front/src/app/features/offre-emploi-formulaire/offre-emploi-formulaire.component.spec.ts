import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OffreEmploiFormulaireComponent } from './offre-emploi-formulaire.component';

describe('OffreEmploiFormulaire', () => {
  let component: OffreEmploiFormulaireComponent;
  let fixture: ComponentFixture<OffreEmploiFormulaireComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OffreEmploiFormulaireComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OffreEmploiFormulaireComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
