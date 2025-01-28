import {Component, Input} from '@angular/core';
import {SpinnerComponent} from './spinner/spinner.component';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'app-progress-bar',
  standalone:true,
  imports: [
    SpinnerComponent,
    CommonModule
  ],
  templateUrl: './progress-bar.component.html',
  styleUrl: './progress-bar.component.css'
})
export class ProgressBarComponent {
  @Input() progress: number = 0;
  @Input() isUploading: boolean = false;
  @Input() progressMessage: string = '';
}
