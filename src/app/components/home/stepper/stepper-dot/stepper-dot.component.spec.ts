import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StepperDotComponent } from './stepper-dot.component';

describe('StepperDotComponent', () => {
  let component: StepperDotComponent;
  let fixture: ComponentFixture<StepperDotComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StepperDotComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StepperDotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
