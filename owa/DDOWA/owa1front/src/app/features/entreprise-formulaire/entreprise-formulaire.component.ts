import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { EntrepriseService, Entreprise } from '../../core/entreprise.service';
import { BehaviorSubject } from 'rxjs';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-entreprise-formulaire',
  templateUrl: './entreprise-formulaire.component.html',
  styleUrls: ['./entreprise-formulaire.component.css'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule]
})
export class EntrepriseFormulaireComponent implements OnInit {
  form: FormGroup;
  isEdit = false;
  entrepriseId: number | null = null;
  file: File | null = null;
  error: string | null = null;
  private loadingSubject = new BehaviorSubject<boolean>(false);
  loading$ = this.loadingSubject.asObservable();

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private entrepriseService: EntrepriseService,
  ) {
    this.form = this.fb.group({
      nom: ['', Validators.required],
      adresse_siege: ['', Validators.required],
      entreprise_infos: [''],
      image: [null]
    });
  }

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (id) {
        this.isEdit = true;
        this.entrepriseId = +id;
        this.loadingSubject.next(true);
        this.entrepriseService.getOne(this.entrepriseId).subscribe({
          next: (ent: Entreprise) => {
            this.form.patchValue(ent);
            this.loadingSubject.next(false);
          },
          error: () => {
            this.error = "Erreur lors du chargement.";
            this.loadingSubject.next(false);
          }
        });
      }
    });
  }

  onFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length) {
      this.file = input.files[0];
    }
  }

  onSubmit() {
    if (this.form.invalid) return;
    this.loadingSubject.next(true);
    this.error = null;
    const values = this.form.value;
    let obs$;
    if (this.isEdit && this.entrepriseId) {
      obs$ = this.entrepriseService.update(this.entrepriseId, values, this.file!);
    } else {
      obs$ = this.entrepriseService.create(values, this.file!);
    }
    obs$.subscribe({
      next: () => {
        this.loadingSubject.next(false);
        this.router.navigate(['/entreprise']);
      },
      error: () => {
        this.error = "Erreur lors de la " + (this.isEdit ? "modification." : "création.");
        this.loadingSubject.next(false);
      }
    });
  }
}
