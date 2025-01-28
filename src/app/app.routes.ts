import { Routes } from '@angular/router'
import {HomeComponent} from './pages/home/home.component';
import {FeaturesComponent} from './pages/features/features.component';
import {ServicesComponent} from './pages/services/services.component';
import {AboutComponent} from './pages/about/about.component';

const routeConfig: Routes = [
  {
    path: '',
    component: HomeComponent,
    title: 'Home page',
  },
  {
    path: 'features',
    component: FeaturesComponent,
    title: 'Features'
  },
  {
    path: 'services',
    component: ServicesComponent,
    title: 'Services'
  },
  {
    path: 'about',
    component: AboutComponent,
    title: 'About'
  }
];
export default routeConfig;
