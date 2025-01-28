import {Component, OnInit} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';
import {Category, SpringCategoriesService} from '../../../../../services/spring-services/spring-categories.service';
import {SpringBootService} from '../../../../../services/spring-services/spring-generate-project.service';



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

  constructor(private springCategoriesService : SpringCategoriesService, private springGenerate : SpringBootService) {}

  ngOnInit(): void {
    this.categories = this.springCategoriesService.getCategories();
    this.activeTab = this.categories[0]?.name || '';
  }

  handleCheckboxChange(id: string | undefined): void {
    if (!id) {
      console.warn('ID is undefined. Skipping...');
      return;
    }
    // Ajoutez ici votre logique
    const index = this.selectedOptions.indexOf(id);
    if (index > -1) {
      this.selectedOptions.splice(index, 1); // Décocher
    } else {
      this.selectedOptions.push(id); // Cocher
    }
  }

  async handleConnect(): Promise<void> {
    if (this.selectedOptions.length > 0) {
      try {
        const dependencies = this.selectedOptions.join(',');
        console.log(`dependencies ${dependencies}`);

        const blob = await this.springGenerate.generateProject(
          dependencies,
          'com.example',
          'test',
          'test',
          'description',
          21
        );

        this.springGenerate.downloadFile(blob, 'pom.xml');
        this.openModal = false;

      } catch (error) {
        console.error('Erreur lors de la génération du projet:', error);
      }
    }
  }
}
