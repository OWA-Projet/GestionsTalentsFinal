import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserFormulaireComponent } from './utilisateur-form.component';

describe('UtilisateurFormComponent', () => {
  let component: UserFormulaireComponent;
  let fixture: ComponentFixture<UserFormulaireComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserFormulaireComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserFormulaireComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
