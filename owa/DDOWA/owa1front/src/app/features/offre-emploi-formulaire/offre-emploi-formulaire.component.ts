import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { OffreEmploiService, OffreEmploi } from '../../core/offres.service';
import { BehaviorSubject } from 'rxjs';
import { ReactiveFormsModule } from '@angular/forms';

import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-offre-emploi-formulaire',
  templateUrl: './offre-emploi-formulaire.component.html',
  styleUrls: ['./offre-emploi-formulaire.component.css'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule]
})
export class OffreEmploiFormulaireComponent implements OnInit {
  form: FormGroup;
  isEdit = false;
  offreId: number | null = null;
  file: File | null = null;
  error: string | null = null;
  entreprisename: string = '';

  /** Loader réactif */
  private loadingSubject = new BehaviorSubject<boolean>(false);
  loading$ = this.loadingSubject.asObservable();

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private offreService: OffreEmploiService,
  ) {
    this.form = this.fb.group({
      libelle: ['', Validators.required],
      description: [''],
      metier_propose: ['', Validators.required],
      secteur_activite: ['', Validators.required],
      Experience_requise: ['', Validators.required],
      niveau_etude: ['', Validators.required],
      type_contrat: ['', Validators.required],
      date_publication: ['', Validators.required],
      date_expiration: ['', Validators.required],
      profil_recherche: [''],
      entreprise_id: [null, Validators.required],
      image: [null]
    });
  }

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      const identreprise = params.get('identreprise');
      if (id) {
        this.isEdit = true;
        this.offreId = +id;
        this.loadingSubject.next(true);
        this.offreService.getOne(this.offreId).subscribe({
          next: (offre: OffreEmploi) => { 
            this.entreprisename = offre.entreprise?.nom || '';
            this.form.patchValue({
              ...offre,
              entreprise_id: offre.entreprise?.id ?? null,
              date_publication: offre.date_publication ? offre.date_publication.slice(0, 10) : '',
              date_expiration: offre.date_expiration ? offre.date_expiration.slice(0, 10) : ''
            });
            this.loadingSubject.next(false);
          },
          error: () => {
            this.error = "Erreur lors du chargement de l'offre.";
            this.loadingSubject.next(false);
          }
        });
      } else if (identreprise) {
        this.form.patchValue({ entreprise_id: +identreprise });
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
    const offre: OffreEmploi = {
      ...values,
      entreprise_id: +values.entreprise_id,
    };
    console.log("loading1")
    let obs$

    if (this.isEdit && this.offreId) {
      obs$ = this.offreService.update(this.offreId, offre, this.file!);
    } else {
      console.log("create")
      // Tu veux récupérer identreprise depuis l'URL si besoin
      const identreprise = this.route.snapshot.paramMap.get('identreprise');
      if (identreprise) {
        offre.entreprise_id = +identreprise; // Affecte le bon id d'entreprise à l'offre
      }
      obs$ = this.offreService.create(offre, this.file!);
    }
    obs$.subscribe({
      next: () => {
        console.log("loading")
        this.loadingSubject.next(false);
        this.router.navigate(['/offres-rh']);
        // message de succès si besoin
      },
      error: () => {
        this.error = "Erreur lors de la " + (this.isEdit ? "modification." : "ajout.");
        this.loadingSubject.next(false);
      }
    });
  }
}
