import {Component, Input} from '@angular/core';
import {CommonModule} from '@angular/common';
import {StepperDotComponent} from './stepper-dot/stepper-dot.component';
import {Step} from '../../../models/step';

@Component({
  selector: 'app-stepper',
  imports: [CommonModule, StepperDotComponent],
  standalone: true,
  templateUrl: './stepper.component.html',
  styleUrl: './stepper.component.css'
})
export class StepperComponent {
  @Input() steps: Step[] = [];
  @Input() currentStep: number = 1;
  @Input() layout: 'horizontal' | 'vertical' = 'horizontal';

  getProgress(): string {
    return `${((this.currentStep - 1) / (this.steps.length - 1)) * 100}%`;
  }

  isStepActive(index: number): boolean {
    return index + 1 === this.currentStep;
  }

  isStepCompleted(index: number): boolean {
    return index + 1 < this.currentStep;
  }
}
