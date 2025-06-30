import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CvOffresComponent } from './cv-offres.component';

describe('CvOffresComponent', () => {
  let component: CvOffresComponent;
  let fixture: ComponentFixture<CvOffresComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CvOffresComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CvOffresComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
