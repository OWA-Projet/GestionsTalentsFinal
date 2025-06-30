import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EntrepriseFormulaireComponent } from './entreprise-formulaire.component';

describe('EntrepriseFormulaireComponent', () => {
  let component: EntrepriseFormulaireComponent;
  let fixture: ComponentFixture<EntrepriseFormulaireComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EntrepriseFormulaireComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EntrepriseFormulaireComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
