import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OffreDetailComponent } from './offre-detail';

describe('OffreDetail', () => {
  let component: OffreDetailComponent;
  let fixture: ComponentFixture<OffreDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OffreDetailComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OffreDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
