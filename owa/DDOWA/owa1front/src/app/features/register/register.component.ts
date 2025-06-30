import { Component } from '@angular/core';
import { FormBuilder, Validators, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../../core/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  standalone: true,
  imports: [ReactiveFormsModule], // AJOUT ICI
})
export class RegisterComponent {
  registerForm: FormGroup;
  loading = false;
  success: string | null = null;
  error: string | null = null;

  constructor(private fb: FormBuilder, private auth: AuthService, private router: Router) {
    // <--- L'initialisation doit être dans le constructeur
    this.registerForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(4)]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      nom: ['', Validators.required],
      prenom: ['', Validators.required],
      poste: ['', Validators.required],
    });
  }

  onSubmit() {
    if (this.registerForm.invalid) return;

    this.loading = true;
    this.success = null;
    this.error = null;

    // Corriger ici : forcer la conversion vers string, pas string | null
    const raw = this.registerForm.value;
    const payload = {
      username: raw.username ?? '',
      password: raw.password ?? '',
      nom: raw.nom ?? '',
      prenom: raw.prenom ?? '',
      poste: raw.poste ?? '',
      roles: ['CANDIDAT'],
    };

    this.auth.register(payload).subscribe({
      next: _ => {
        this.success = "Votre compte a bien été créé !";
        this.loading = false;
        this.registerForm.reset();
        setTimeout(() => {
      this.router.navigate(['/login']); // Ou n'importe quelle route cible
    }, 4000);
      },
      error: err => {
        this.error = err.error?.detail || "Erreur lors de l'inscription.";
        this.loading = false;
      }
    });
  }

  get f() { return this.registerForm.controls; }
}
