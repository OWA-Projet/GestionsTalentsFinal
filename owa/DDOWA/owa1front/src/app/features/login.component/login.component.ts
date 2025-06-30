import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../../core/auth.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule]
})
export class LoginComponent {
  loginForm: FormGroup;
  loading = false;
  alertMsg: string | null = null;
  alertType: 'success' | 'error' = 'success';

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  setAlert(message: string, type: 'success' | 'error') {
    this.alertMsg = message;
    this.alertType = type;
    setTimeout(() => this.alertMsg = null, 3000);
  }

  onSubmit() {
    if (this.loginForm.invalid) return;

    this.loading = true;
    this.auth.login({
      username: this.loginForm.value.username,
      password: this.loginForm.value.password
    }).subscribe({
      next: () => {
        this.loading = false;
        this.setAlert("Connexion réussie !", 'success');
        setTimeout(() => {
          this.alertMsg = null;

        const userStr = localStorage.getItem('user');
        let user: any = null;
        try {
        user = userStr ? JSON.parse(userStr) : null;
        } catch {
        user = null;
        }

    // Vérifier le rôle
        const isRh = Array.isArray(user?.roles) && user.roles.includes('RH');
        
        
         
          
          this.router.navigate(['/']);
          
        }, 3000);
      },
      error: (err) => {
        this.loading = false;
        this.setAlert(err?.error?.error || "Échec de connexion. Vérifiez vos identifiants.", 'error');
      }
    });
  }
}
