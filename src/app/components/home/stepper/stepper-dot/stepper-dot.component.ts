import {Component, Input} from '@angular/core';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'app-stepper-dot',
  imports: [CommonModule],
  standalone: true,
  templateUrl: './stepper-dot.component.html',
  styleUrl: './stepper-dot.component.css'
})
export class StepperDotComponent {
  @Input() step!: string | undefined;
  @Input() isActive: boolean = false;
  @Input() isCompleted: boolean = false;
}
