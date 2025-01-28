import { Injectable } from '@angular/core';
import {Step} from '../../models/step';

@Injectable({
  providedIn: 'root'
})
export class StepService {

  private steps: Step[] = [
    { label: 'Prepare Files', icon: '1', content: 'Upload and prepare your .drawio files for processing.' },
    { label: 'Setting up the projet', icon: '2', content: 'Configure the name of the project and dependencies' },
    { label: 'Uploading', icon: '3', content: 'Files are being uploaded to the server. Please wait.' },
    { label: 'Processing', icon: '4', content: 'Your files are being processed. This may take some time.' },
    { label: 'Download', icon: '5', content: 'Upload complete! Download your generated code files.' }
  ];

  constructor() {}

  // Recuperer les etapes
  getSteps(): Step[] {
    return this.steps;
  }
}

