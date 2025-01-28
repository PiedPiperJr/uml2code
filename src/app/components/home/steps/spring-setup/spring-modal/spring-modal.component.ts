import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {Category, SpringCategoriesService} from '../../../../../services/spring-services/spring-categories.service';

@Component({
  selector: 'app-spring-modal',
  imports: [CommonModule, FormsModule],
  standalone: true,
  templateUrl: './spring-modal.component.html',
  styleUrl: './spring-modal.component.css'
})
export class SpringModalComponent implements OnInit {
  categories: Category[] = [];
  selectedOptions: string[] = [];
  activeTab: string =  '';
  openModal = false;

  @Input() dependencies : string | undefined = '';
  @Output() dependenciesChange = new EventEmitter<string>();

  constructor(private springCategoriesService : SpringCategoriesService) {}

  ngOnInit(): void {
    this.categories = this.springCategoriesService.getCategories();
    this.activeTab = this.categories[0]?.name || '';
    if (this.dependencies) {
      this.selectedOptions = this.dependencies.split(',');
    }
  }

  updateDependencies(): void {
    this.dependencies = this.selectedOptions.join(',');
    console.log(`Spring Modal dependencies : ${this.dependencies}`)
    this.dependenciesChange.emit(this.dependencies);
  }

  handleCheckboxChange(id: string | undefined): void {
    if (!id) {
      console.warn('ID is undefined. Skipping...');
      return;
    }
    const index = this.selectedOptions.indexOf(id);
    if (index > -1) {
      this.selectedOptions.splice(index, 1);
    } else {
      this.selectedOptions.push(id);
    }

    this.updateDependencies();
  }

  async handleConnect(): Promise<void> {
    if (this.selectedOptions.length > 0) {
      this.openModal = false;
    }
  }
}
