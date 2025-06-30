import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ContactService } from '../../core/contact.service';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule]
})
export class ContactComponent {
  form: FormGroup;
  successMsg: string | null = null;
  errorMsg: string | null = null;
  isLoading = false;

  constructor(private fb: FormBuilder, private contactService: ContactService) {
    this.form = this.fb.group({
      nom: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      sujet: ['', Validators.required],
      message: ['', [Validators.required, Validators.minLength(10)]]
    });
  }

  onSubmit() {
    if (this.form.invalid) return;
    this.isLoading = true;
    this.successMsg = null;
    this.errorMsg = null;

    this.contactService.envoyerContact(this.form.value).subscribe({
      next: () => {
        this.isLoading = false;
        this.successMsg = "Votre message a bien été envoyé. Merci !";
        this.form.reset();
      },
      error: () => {
        this.isLoading = false;
        this.errorMsg = "Erreur lors de l’envoi. Réessayez plus tard.";
      }
    });
  }
}
