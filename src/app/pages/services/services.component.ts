import { Component } from '@angular/core';
import {CommonModule} from '@angular/common';
import {RouterModule} from '@angular/router';
import {animate, query, stagger, style, transition, trigger} from '@angular/animations';

@Component({
  selector: 'app-services',
  imports: [CommonModule, RouterModule],
  standalone: true,
  templateUrl: './services.component.html',
  styleUrl: './services.component.css',
  animations: [
    trigger('staggerFade', [
      transition('* => *', [
        query(':enter', [
          style({ opacity: 0, transform: 'translateY(20px)' }),
          stagger(100, [
            animate('0.5s ease', style({ opacity: 1, transform: 'translateY(0)' }))
          ])
        ], { optional: true })
      ])
    ])
  ]
})
export class ServicesComponent {
  services = [
    {
      icon: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4',
      title: 'UML Diagram Processing',
      description: 'Upload and process your UML diagrams with our advanced recognition system that understands complex class relationships and interactions.',
      colorClass: {
        bg: 'bg-blue-100',
        text: 'text-blue-600'
      }
    },
    {
      icon: 'M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
      title: 'Code Generation',
      description: 'Transform your diagrams into clean, well-structured code that follows best practices and design patterns.',
      colorClass: {
        bg: 'bg-indigo-100',
        text: 'text-indigo-600'
      }
    },
    {
      icon: 'M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4',
      title: 'Customization Options',
      description: 'Tailor the output to your needs with extensive configuration options for different frameworks and architectures.',
      colorClass: {
        bg: 'bg-purple-100',
        text: 'text-purple-600'
      }
    }
    ];
}
