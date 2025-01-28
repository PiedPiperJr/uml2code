import {Component, Input} from '@angular/core';
import {CommonModule} from '@angular/common';
import {UploadedFile} from '../../../../models/uploaded-file';

@Component({
  selector: 'app-download-files',
  imports: [CommonModule],
  standalone: true,
  templateUrl: './download-files.component.html',
  styleUrl: './download-files.component.css'
})
export class DownloadFilesComponent {
  @Input() files: UploadedFile[] = [];
  @Input() downloadLinks: string[] = [];
}
