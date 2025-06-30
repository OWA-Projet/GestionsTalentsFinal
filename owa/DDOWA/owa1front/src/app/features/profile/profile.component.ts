import { Component, OnInit } from '@angular/core';
import { UserService, User } from '../../core/user.service';
import { Observable } from 'rxjs';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-profil-utilisateur',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class ProfilUtilisateurComponent implements OnInit {
  user$!: Observable<User | null>;


  constructor(private userService: UserService) {}

  ngOnInit() {
    this.user$ = this.userService.getCurrentUser();
  }
  get currentUser(): any {
    const userStr = localStorage.getItem('user');
    try {
      return userStr ? JSON.parse(userStr) : null;
    } catch {
      return null;
    }
  }

  isRH(): boolean {
    return Array.isArray(this.currentUser?.roles) && this.currentUser.roles.includes('RH');
  }
}
