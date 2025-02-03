import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PrepareFileComponent } from '../../components/home/steps/prepare-file/prepare-file.component';
import { Step } from '../../models/step';
import { StepService } from '../../services/stepper/step.service';
import { UploadedFile } from '../../models/uploaded-file';
import { StepperComponent } from '../../components/home/stepper/stepper.component';
import { DownloadFilesComponent } from '../../components/home/steps/download-files/download-files.component';
import { ProcessingProgressComponent } from '../../components/home/steps/processing-progress/processing-progress.component';
import { UploadProgressComponent } from '../../components/home/steps/upload-progress/upload-progress.component';
import { SpringSetupComponent } from '../../components/home/steps/spring-setup/spring-setup.component';
import { SpringBootFormData } from '../../models/spring-boot-form-data';
import { ServerInput } from '../../models/server-input';
import { UploadProgress, UploadServiceService } from '../../services/upload-to-server/upload-service.service';
import { HttpEventType, HttpResponse } from '@angular/common/http';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    PrepareFileComponent,
    StepperComponent,
    DownloadFilesComponent,
    ProcessingProgressComponent,
    UploadProgressComponent,
    SpringSetupComponent,
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
  formData: SpringBootFormData = {
    groupId: '',
    artifactId: '',
    name: '',
    packageName: '',
    packaging: 'jar',
    javaVersion: '17',
    description: '',
    dependencies: '',
  };
  selectedFramework: string = "";
  laravelProjectName: string = '';
  serverInputFile: ServerInput | undefined;
  processingError: string | null = null;

  constructor(
    private stepService: StepService,
    private uploadService: UploadServiceService
  ) {}

  ngOnInit(): void {
    this.steps = this.stepService.getSteps();
  }

  onFilesChange(files: UploadedFile[]): void {
    this.files = files;
    this.processingError = null;
  }

  setup(): void {
    this.currentStep = 2;
  }

  onFormDataChange(newData: SpringBootFormData): void {
    this.formData = { ...this.formData, ...newData };
  }

  onFrameworkChange(framework: string): void {
    this.selectedFramework = framework;
  }

  parsingFiles(): void {
    if (this.selectedFramework === 'laravel') {
      this.serverInputFile = {
        files: this.files,
        type: 'laravel',
        project_name: this.laravelProjectName
      };
    } else if (this.selectedFramework === 'springboot') {
      this.serverInputFile = {
        files: this.files,
        type: 'springboot',
        pomxml_url: `https://start.spring.io/pom.xml?groupId=${this.formData.groupId}&artifactId=${this.formData.artifactId}&name=${this.formData.name}&packageName=${this.formData.packageName}&packaging=${this.formData.packaging}&javaVersion=${this.formData.javaVersion}&description=${this.formData.description}&dependencies=${this.formData.dependencies}`,
        spring_data: this.formData
      };
    }
  }

  async uploadFiles(): Promise<void> {
    if (this.currentStep === 1) {
      this.currentStep = 2;
      return;
    }

    this.parsingFiles();
    if (!this.serverInputFile) {
      console.error('Server input data not prepared');
      this.processingError = 'Error: Server input data not prepared';
      return;
    }

    this.currentStep = 3;

    try {
      for (const file of this.files) {
        this.fileProgresses[file.file.name] = 0;

        this.uploadService.uploadFileWithProgress(file.file, this.serverInputFile)
          .subscribe({
            next: (progressData: UploadProgress) => {
              console.log(`Progress for ${file.file.name}:`, progressData.progress);
              this.fileProgresses[file.file.name] = progressData.progress;

              if (progressData.downloadUrl) {
                this.downloadLinks.push(progressData.downloadUrl);
                
                // Move to final step when all files are complete
                if (Object.values(this.fileProgresses).every(progress => progress === 100)) {
                  this.currentStep = 5;
                }
              }
            },
            error: (error) => {
              console.error('Upload error:', error);
              this.processingError = `Error processing ${file.file.name}: ${error.message}`;
              this.fileProgresses[file.file.name] = 0;
            }
          });
      }
    } catch (error: any) {
      console.error('Upload error:', error);
      this.processingError = `Error during upload: ${error.message}`;
    }
  }

  handleReset(): void {
    this.files = [];
    this.fileProgresses = {};
    this.processingProgresses = {};
    this.downloadLinks = [];
    this.currentStep = 1;
    this.processingError = null;
    
    // Clean up object URLs
    this.downloadLinks.forEach(url => {
      window.URL.revokeObjectURL(url);
    });
  }

  goToPreviousStep(): void {
    if (this.currentStep > 1) {
      this.currentStep--;
    }
  }

  laravelProjectNameChange(name: string): void {
    this.laravelProjectName = name;
  }

  // Clean up resources when component is destroyed
  ngOnDestroy(): void {
    this.downloadLinks.forEach(url => {
      window.URL.revokeObjectURL(url);
    });
  }
}