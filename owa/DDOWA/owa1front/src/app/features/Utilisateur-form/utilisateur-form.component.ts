import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService, User, EntrepriseLight } from '../../core/user.service';
import { BehaviorSubject } from 'rxjs';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-formulaire',
  templateUrl: './utilisateur-form.component.html',
  styleUrls: ['./utilisateur-form.component.css'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule]
})
export class UserFormulaireComponent implements OnInit {
  form: FormGroup;
  isEdit = false;
  userId: number | null = null;
  error: string | null = null;
  entreprises: EntrepriseLight[] = [];
  private loadingSubject = new BehaviorSubject<boolean>(false);
  loading$ = this.loadingSubject.asObservable();

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private userService: UserService
  ) {
    this.form = this.fb.group({
      username: ['', Validators.required],
      password: [''], // obligatoire à la création, facultatif en édition
      nom: ['', Validators.required],
      prenom: ['', Validators.required],
      poste: ['', Validators.required],
      roles: [[], Validators.required],
      entreprise: [null]
    });
  }

  ngOnInit() {
    // Charger la liste des entreprises pour la dropdown
    this.userService.getEntreprises().subscribe({
      next: (data) => this.entreprises = data,
      error: () => this.error = "Erreur lors du chargement des entreprises."
    });

    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (id) {
        this.isEdit = true;
        this.userId = +id;
        this.loadingSubject.next(true);
        this.userService.getOne(this.userId).subscribe({
          next: (user: User) => {
            this.form.patchValue({
              ...user,
              entreprise: user.entreprise ? user.entreprise.id : null,
              password: '' // Jamais prérempli en édition
            });
            this.loadingSubject.next(false);
          },
          error: () => {
            this.error = "Erreur lors du chargement de l'utilisateur.";
            this.loadingSubject.next(false);
          }
        });
      }
    });
  }

  onSubmit() {
    if (this.form.invalid) return;
    this.loadingSubject.next(true);
    this.error = null;
    const values = this.form.value;
    // Préparation du payload pour le backend DRF :
    const toSend: any = {
      ...values,
      entreprise_id: values.entreprise || null,
      roles: Array.isArray(values.roles) ? values.roles : [values.roles]
    };
    // Ne jamais envoyer 'entreprise' (read_only) !
    delete toSend.entreprise;
    // En édition : si password vide, ne pas l'envoyer
    if (this.isEdit && !toSend.password) {
      delete toSend.password;
    }
    let obs$;
    if (this.isEdit && this.userId) {
      obs$ = this.userService.update(this.userId, toSend);
    } else {
      obs$ = this.userService.create(toSend);
    }
    obs$.subscribe({
      next: () => {
        this.loadingSubject.next(false);
        this.router.navigate(['/user-list']);
      },
      error: (err) => {
        this.error = "Erreur lors de la " + (this.isEdit ? "modification." : "création.");
        this.loadingSubject.next(false);
        console.error('Erreur backend:', err);
        if (err.error && typeof err.error === 'object') {
          this.error += ' ' + JSON.stringify(err.error);
        }
      }
    });
  }
  isRHSelected(): boolean {
  // Vérifie si le rôle RH est dans la liste des rôles sélectionnés
  return this.form.get('roles')?.value?.includes('RH');
}

}
