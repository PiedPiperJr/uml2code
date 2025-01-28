import { Component } from '@angular/core';
import {CommonModule} from '@angular/common';
import {PrepareFileComponent} from '../../components/home/steps/prepare-file/prepare-file.component';
import {Step} from '../../models/step';
import {StepService} from '../../services/stepper/step.service';
import {UploadedFile} from '../../models/uploaded-file';
import {StepperComponent} from '../../components/home/stepper/stepper.component';
import {DownloadFilesComponent} from '../../components/home/steps/download-files/download-files.component';
import {
  ProcessingProgressComponent
} from '../../components/home/steps/processing-progress/processing-progress.component';
import {UploadProgressComponent} from '../../components/home/steps/upload-progress/upload-progress.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    PrepareFileComponent,
    StepperComponent,
    DownloadFilesComponent,
    ProcessingProgressComponent,
    UploadProgressComponent
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  currentStep = 1;
  steps: Step[] = [];
  files: UploadedFile[] = [];
  downloadLinks: string[] = [];
  fileProgresses: { [key: string]: number } = {};
  processingProgresses: { [key: string]: number } = {};
  layout: 'horizontal' | 'vertical' = 'horizontal';

  constructor(private stepService: StepService) {}

  ngOnInit(): void {
    this.steps = this.stepService.getSteps();
  }

  onFilesChange(files: UploadedFile[]): void {
    this.files = files;
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
          if (Object.values(this.fileProgresses).every(progress => progress === 100)) {
            this.currentStep = 3;
            this.processFiles();
          }
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
          if (Object.values(this.processingProgresses).every(progress => progress === 100)) {
            this.generateDownloadLinks();
            this.currentStep = 4;
          }
        }
      }, 500);
    });
  }

  generateDownloadLinks(): void {
    this.downloadLinks = this.files.map(file =>
      `assets/generated/${file.file.name.replace('.drawio', '.zip')}`
    );
  }

  handleReset(): void {
    this.files = [];
    this.fileProgresses = {};
    this.processingProgresses = {};
    this.downloadLinks = [];
    this.currentStep = 1;
  }

    goToPreviousStep(): void {
      if (this.currentStep > 1) {
        this.cancelCurrentStep();
        this.currentStep--;
      }
    }

  cancelCurrentStep(): void {
    switch (this.currentStep) {
      case 2:
        this.fileProgresses = {};
        console.log("Upload annulé.");
        break;

      case 3:
        this.processingProgresses = {};
        console.log("Processing annulé.");
        break;

      case 4:
        this.downloadLinks = [];
        console.log("Téléchargement annulé.");
        break;
    }
  }
}
