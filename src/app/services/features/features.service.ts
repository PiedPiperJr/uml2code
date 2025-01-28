import { Injectable } from '@angular/core';
import {Feature} from '../../models/features';

@Injectable({
  providedIn: 'root'
})
export class FeaturesService {

  private features: Feature[] = [
    {
      // Icône de téléchargement
      icon: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12',
      title: 'Upload UML Diagram',
      description: 'Easily upload UML diagrams (class diagrams, use case diagrams) to kickstart the process.',
      colorClass: {
        bg: 'bg-indigo-100',
        text: 'text-indigo-600'
      },
      isVisible: true
    },
    {
      // Icône de code/génération
      icon: 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4',
      title: 'Automatic Code Generation',
      description: 'Generate a working alpha version of the code in seconds.',
      colorClass: {
        bg: 'bg-green-100',
        text: 'text-green-600'
      },
      isVisible: true
    },
    {
      // Icône de technologie/framework
      icon: 'M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
      title: 'Spring Boot & Laravel Support',
      description: 'Choose your preferred framework: Java Spring Boot or PHP Laravel.',
      colorClass: {
        bg: 'bg-blue-100',
        text: 'text-blue-600'
      },
      isVisible: true
    },
    {
      // Icône de personnalisation/réglages
      icon: 'M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4',
      title: 'Customizable Templates',
      description: 'Fine-tune the generated code by adding dependencies in your Spring Boot project.',
      colorClass: {
        bg: 'bg-yellow-100',
        text: 'text-yellow-600'
      },
      isVisible: true
    },
    {
      // Icône de mise à jour/progrès
      icon: 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15',
      title: 'Future-Proof',
      description: 'Regular updates to support more frameworks and new UML standards.',
      colorClass: {
        bg: 'bg-purple-100',
        text: 'text-purple-600'
      },
      isVisible: true
    }
    ,
    {
      icon: 'M12 18v-6m0 6l-3-3m3 3l3-3M3 6h18M9 6h6',
      title: 'Enhanced Export Options',
      description: 'Easily download code in ZIP files.',
      colorClass: {
        bg: 'bg-teal-100',
        text: 'text-teal-600'
      },
      isVisible: true
    }];

  constructor() { }

  getFeatures(): Feature[] {
    return this.features
  }
}
