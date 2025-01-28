import {Component, EventEmitter, Input, Output} from '@angular/core';
import {CommonModule} from '@angular/common';
import {UploadedFile} from '../../../../models/uploaded-file';

@Component({
  selector: 'app-prepare-file',
  imports: [CommonModule],
  standalone: true,
  templateUrl: './prepare-file.component.html',
  styleUrl: './prepare-file.component.css'
})
export class PrepareFileComponent {
  @Input() files: UploadedFile[] = [];
  @Output() filesChange = new EventEmitter<UploadedFile[]>();
  @Output() startUpload = new EventEmitter<void>();

  dropZoneClass = 'border-2 border-dashed border-gray-300 rounded-lg p-12 text-center cursor-pointer hover:border-indigo-500 transition-colors';

  onSelectFile(): void {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.drawio';
    fileInput.multiple = true;
    fileInput.onchange = (event: Event) => {
      const target = event.target as HTMLInputElement;
      if (target.files) {
        this.handleFiles(Array.from(target.files));
      }
    };
    fileInput.click();
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.dropZoneClass = 'border-2 border-dashed border-indigo-500 rounded-lg p-12 text-center cursor-pointer bg-indigo-50 transition-colors';
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.dropZoneClass = 'border-2 border-dashed border-gray-300 rounded-lg p-12 text-center cursor-pointer hover:border-indigo-500 transition-colors';
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.dropZoneClass = 'border-2 border-dashed border-gray-300 rounded-lg p-12 text-center cursor-pointer hover:border-indigo-500 transition-colors';

    if (event.dataTransfer?.files) {
      this.handleFiles(Array.from(event.dataTransfer.files));
    }
  }

  onRemoveFile(fileId: string): void {
    this.files = this.files.filter(file => file.id !== fileId);
    this.filesChange.emit(this.files);
  }

  protected handleFiles(files: File[]): void {
    const newFiles = files.map(file => ({
      id: crypto.randomUUID(),
      file: file
    }));
    this.files = [...this.files, ...newFiles];
    this.filesChange.emit(this.files);
  }

  trackByFn(index: number, item: UploadedFile): string {
    return item.id;
  }

  onSelectDescription(): void {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.txt,.doc,.docx,.pdf';
    fileInput.multiple = false;
    fileInput.onchange = (event: Event) => {
      const target = event.target as HTMLInputElement;
      if (target.files) {
        this.handleFiles(Array.from(target.files));
      }
    };
    fileInput.click();
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  removeFile(fileId: string): void {
    this.files = this.files.filter(file => file.id !== fileId);
  }
}
