import {Component, Input} from '@angular/core';
import {ProgressBarComponent} from '../../progress-bar/progress-bar.component';
import {UploadedFile} from '../../../../models/uploaded-file';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'app-processing-progress',
  imports: [
    ProgressBarComponent,
    CommonModule
  ],
  standalone: true,
  templateUrl: './processing-progress.component.html',
  styleUrl: './processing-progress.component.css'
})
export class ProcessingProgressComponent {
  @Input() files: UploadedFile[] = [];
  @Input() processingProgresses: { [key: string]: number } = {};
}
