import { Component } from '@angular/core';
import {FormsModule} from '@angular/forms';
import {ProgressBarComponent} from '../progress-bar/progress-bar.component';
import {StepperComponent} from '../stepper/stepper.component';
import {CommonModule} from '@angular/common';
import {Step} from '../../../models/step';
import {StepService} from '../../../services/stepper/step.service';

interface UploadedFile {
  id: string;
  file: File;
  diagramUrl?: string;
  descriptionFileName?: string;
}

@Component({
  selector: 'app-prepare-files',
  standalone: true,
  imports: [FormsModule, ProgressBarComponent, StepperComponent, CommonModule],
  templateUrl: './prepare-files.component.html',
  styleUrl: './prepare-files.component.css'
})
export class PrepareFilesComponent {

  currentStep = 1;
  steps: Step[] = [];
  files: UploadedFile[] = [];
  downloadLinks: string[] = [];
  fileProgresses: { [key: string]: number } = {};
  processingProgresses: { [key: string]: number } = {};
  layout: 'horizontal' | 'vertical' = 'horizontal';
  dropZoneClass = 'border-2 border-dashed border-gray-300 rounded-lg p-12 text-center cursor-pointer hover:border-indigo-500 transition-colors';

  constructor(private stepService: StepService) {}

  ngOnInit(): void {
    this.steps = this.stepService.getSteps();
  }

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

  removeFile(fileId: string): void {
    this.files = this.files.filter(file => file.id !== fileId);
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

  private handleFiles(files: File[]): void {
    files.forEach(file => {
      const newFile: UploadedFile = {
        id: crypto.randomUUID(),
        file: file
      };
      this.files.push(newFile);
    });
  }

  uploadFiles(): void {
    this.currentStep = 2;
    this.files.forEach(file => {
      this.fileProgresses[file.file.name] = 0;
      const interval = setInterval(() => {
        if (this.fileProgresses[file.file.name] < 100) {
          this.fileProgresses[file.file.name] += 10;
        } else {
          clearInterval(interval);
          this.currentStep = 3;
          this.processFiles();
        }
      }, 500);
    });
  }

  processFiles(): void {
    this.files.forEach(file => {
      this.processingProgresses[file.file.name] = 0;
      const interval = setInterval(() => {
        if (this.processingProgresses[file.file.name] < 100) {
          this.processingProgresses[file.file.name] += 10;
        } else {
          clearInterval(interval);
          this.generateDownloadLinks();
          this.currentStep = 4;
        }
      }, 500);
    });
  }

  generateDownloadLinks(): void {
    this.downloadLinks = this.files.map(file => `assets/generated/${file.file.name.replace('.drawio', '.zip')}`);
  }

  handleReset(): void {
    this.files = [];
    this.fileProgresses = {};
    this.processingProgresses = {};
    this.downloadLinks = [];
    this.currentStep = 1;
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

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  trackByFn(index: number, item: UploadedFile): string {
    return item.id;
  }
}
