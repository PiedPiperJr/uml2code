import { Injectable } from '@angular/core';
import {Step} from '../../models/step';

@Injectable({
  providedIn: 'root'
})
export class StepService {

  private steps: Step[] = [
    { label: 'Prepare Files', icon: '1', content: 'Upload and prepare your .drawio files for processing.' },
    { label: 'Uploading', icon: '2', content: 'Files are being uploaded to the server. Please wait.' },
    { label: 'Processing', icon: '3', content: 'Your files are being processed. This may take some time.' },
    { label: 'Download', icon: '4', content: 'Upload complete! Download your generated code files.' }
  ];

  constructor() {}

  // Recuperer les etapes
  getSteps(): Step[] {
    return this.steps;
  }
}

