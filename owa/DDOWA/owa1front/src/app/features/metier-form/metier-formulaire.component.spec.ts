import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MetierFormulaireComponent } from './metier-formulaire.component';

describe('MetierFormulaireComponent', () => {
  let component: MetierFormulaireComponent;
  let fixture: ComponentFixture<MetierFormulaireComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MetierFormulaireComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MetierFormulaireComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
