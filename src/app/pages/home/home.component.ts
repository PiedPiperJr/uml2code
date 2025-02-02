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
import {SpringSetupComponent} from '../../components/home/steps/spring-setup/spring-setup.component';
import {SpringBootFormData} from '../../models/spring-boot-form-data';
import {ServerInput} from '../../models/server-input';

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
  formData : SpringBootFormData = {
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
  serverInputFile : ServerInput = {
    files: [],
    type : '',
    params : ''
  }

  constructor(private stepService: StepService) {}

  ngOnInit(): void {
    this.steps = this.stepService.getSteps();
  }

  onFilesChange(files: UploadedFile[]): void {
    this.files = files;
  }

  setup() :void {
    console.log('Settings')
    this.currentStep = 2
  }

  onFormDataChange(newData: SpringBootFormData): void {
    console.log('Données mises à jour:', newData);
  }

  onFrameworkChange(framework:string): void {
    console.log('... Framework')
  }

  uploadFiles(): void {
    console.log('Uploading files...', this.files);
    if(this.currentStep === 1) {
      this.currentStep = 2;
    } else {
      this.currentStep = 3;
      this.files.forEach(file => {
        this.fileProgresses[file.file.name] = 0;
        const interval = setInterval(() => {
          if (this.fileProgresses[file.file.name] < 100) {
            this.fileProgresses[file.file.name] += 10;
          } else {
            clearInterval(interval);
            if (Object.values(this.fileProgresses).every(progress => progress === 100)) {
              this.currentStep = 4;
              this.processFiles();
            }
          }
        }, 500);
      });
    }
  }

  parsingFiles() : void {
    if (this.selectedFramework === 'laravel'){
      this.serverInputFile = {
        files : this.files,
        type: 'laravel',
        params: this.laravelProjectName
      }
    } else {
      if (this.selectedFramework === 'springboot'){
        this.serverInputFile = {
          files : this.files,
          type : 'springboot',
          params: "https://start.spring.io/pom.xml?groupId=" + this.formData.groupId + "&artifactId=" + this.formData.artifactId + "&name=" + this.formData.name + "&packageName=" + this.formData.packageName + "&packaging=" + this.formData.packaging + "&javaVersion=" + this.formData.javaVersion + "&description=" + this.formData.description + "&dependencies=" + this.formData.dependencies
        }
      }
    }
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
            this.currentStep = 5;
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
        this.currentStep--;
      }
    }

  laravelProjectNameChange(name: string): void {
    console.log("laravel project name : " + name);
  }
}
