import { Component } from '@angular/core';
import {Feature} from '../../models/features';
import {CommonModule} from '@angular/common';
import {FeaturesService} from '../../services/features/features.service';
import {UploadServiceService} from '../../services/upload-to-server/upload-service.service';


@Component({
  selector: 'app-features',
  imports: [CommonModule],
  standalone: true,
  templateUrl: './features.component.html',
  styleUrl: './features.component.css'
})
export class FeaturesComponent {
  features: Feature[] = [];

  constructor(private featuresService: FeaturesService, private test : UploadServiceService) { }

  ngOnInit() {
    this.features = this.featuresService.getFeatures();
    console.log(this.test.getApiStatus())
  }

}
