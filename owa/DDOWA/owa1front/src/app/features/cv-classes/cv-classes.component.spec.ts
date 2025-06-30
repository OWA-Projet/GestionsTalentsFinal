import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CvClassesComponent } from './cv-classes.component';

describe('CvClassesComponent', () => {
  let component: CvClassesComponent;
  let fixture: ComponentFixture<CvClassesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CvClassesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CvClassesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
