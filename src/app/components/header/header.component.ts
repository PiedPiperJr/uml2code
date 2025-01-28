import { Component } from '@angular/core';
import {RouterModule} from '@angular/router';
import {CommonModule} from '@angular/common';

@Component({
  selector: 'app-header',
  standalone : true,
  imports: [RouterModule,CommonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  menuOpen: boolean = false;

  toggleMenu(): void {
    this.menuOpen = !this.menuOpen;
    console.log('Menu state:', this.menuOpen); // Debugging
  }

  closeMenu(): void {
    this.menuOpen = false;
    console.log('Menu closed');
  }
}
