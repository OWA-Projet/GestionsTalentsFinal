import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OffresRhComponent } from './offres-rh.component';

describe('OffresRh', () => {
  let component:  OffresRhComponent;
  let fixture: ComponentFixture<OffresRhComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OffresRhComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OffresRhComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
