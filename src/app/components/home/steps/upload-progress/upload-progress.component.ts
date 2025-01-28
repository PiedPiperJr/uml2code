import {Component, Input} from '@angular/core';
import {ProgressBarComponent} from '../../progress-bar/progress-bar.component';
import {UploadedFile} from '../../../../models/uploaded-file';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'app-upload-progress',
  imports: [
    ProgressBarComponent,
    CommonModule
  ],
  standalone: true,
  templateUrl: './upload-progress.component.html',
  styleUrl: './upload-progress.component.css'
})
export class UploadProgressComponent {
  @Input() files: UploadedFile[] = [];
  @Input() fileProgresses: { [key: string]: number } = {};
}
