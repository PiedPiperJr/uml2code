import {Component, EventEmitter, Input, Output, ViewChild} from '@angular/core';
import {FormsModule, NgForm} from '@angular/forms';
import {CommonModule} from '@angular/common';
import {SpringBootFormData} from '../../../../models/spring-boot-form-data';
import {SpringModalComponent} from './spring-modal/spring-modal.component';


@Component({
  selector: 'app-spring-setup',
  imports: [CommonModule, FormsModule, SpringModalComponent],
  standalone:true,
  templateUrl: './spring-setup.component.html',
  styleUrl: './spring-setup.component.css'
})
export class SpringSetupComponent {
  @ViewChild('setupForm') setupForm!: NgForm;
  @Input() formData : SpringBootFormData = {};
  @Output() formDataChange = new EventEmitter<SpringBootFormData>();
  @Input() selectedFramework: string = "";
  @Output() selectedFrameworkChange = new EventEmitter<string>();

  @Input() laravelProjectName: string = "";
  @Output() laravelProjectNameChange = new EventEmitter<string>();

  onFieldChange() {
    this.formDataChange.emit(this.formData);
  }

  onFrameworkChange(event: Event): void {
    const select = event.target as HTMLSelectElement;
    const value = select.value;
    this.selectedFramework = value;
    this.selectedFrameworkChange.emit(value);
  }

  onLaravelProjectNameChange(event:Event) : void{
    const input = event.target as HTMLInputElement;
    const value = input.value;
    this.laravelProjectName = value;
    this.laravelProjectNameChange.emit(value);
  }

  // Available options for select fields
  packagingOptions = [
    { value: 'jar', label: 'Jar' },
    { value: 'war', label: 'War' }
  ];

  javaVersionOptions = [
    { value: '23', label: 'Java 23' },
    { value: '21', label: 'Java 21' },
    { value: '17', label: 'Java 17 (LTS)' }
  ];

  onSubmit() {
    if (this.setupForm.valid) {
      console.log('Form submitted:', this.formData);
    }
  }

  resetForm() {
    this.setupForm.resetForm({
      packaging: 'jar',
      javaVersion: '17'
    });
  }
}
