import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CvService } from '../../core/cv.service';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-postuler',
  templateUrl: './postuler.html',
  styleUrls: ['./postuler.css'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
})
export class PostulerComponent {
  postulerForm: FormGroup;
  fichier: File | null = null;
  success: boolean | null = null;
  loading = false;
  error: string | null = null;
  offreId: number ;

  constructor(
    private fb: FormBuilder,
    private cvService: CvService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.postulerForm = this.fb.group({
      formations: ['', Validators.required],
      experiences: ['', Validators.required],
      competences: ['', Validators.required],
      langues: [''],
      permis_conduite: [''],
      fichier: [null, Validators.required]
    });

    // ID offre transmis en param de route (ex: /postuler/:offreId)
    this.offreId = Number(this.route.snapshot.paramMap.get('id')) || 0;
  }

  onFileChange(event: any) {
    if (event.target.files && event.target.files.length > 0) {
      this.fichier = event.target.files[0];
      this.postulerForm.patchValue({ fichier: this.fichier });
      // Pour marquer le champ "touché"
      this.postulerForm.get('fichier')?.markAsTouched();
    }
  }

  onSubmit() {
    this.error = null;
    if (this.postulerForm.invalid || !this.fichier) {
      this.postulerForm.markAllAsTouched();
      return;
    }
    this.loading = true;
    const fd = new FormData();

    // Ajout des champs du form
    fd.append('formations', this.postulerForm.value.formations);
    fd.append('experiences', this.postulerForm.value.experiences);
    fd.append('competences', this.postulerForm.value.competences);
    fd.append('langues', this.postulerForm.value.langues ?? '');
    fd.append('permis_conduite', this.postulerForm.value.permis_conduite ?? '');
    fd.append('fichier', this.fichier);

    // ManyToMany (offres): sous forme d'array, ou juste l'id
    fd.append('offres', String(this.offreId));
    console.log(String(this.offreId))

    // Ajoute l'id du user courant (backend exige owner, donc adapter ici selon ton contexte d'auth)
    const userString = localStorage.getItem('user');
    const userObj = userString ? JSON.parse(userString) : null;
    if (!userObj?.id) {
      this.error = "Utilisateur non connecté ou id manquant";
      this.loading = false;
      return;
    }
    fd.append('owner', userObj.id);
    fd.append('owner_id', String(userObj.id));
    console.log(fd);
    this.cvService.createCVcandidat(fd).subscribe({
      next: () => {
        console.log("hhhhhhhhhhhhhhhhhhh");
        this.success = true;
        this.loading = false;
        this.postulerForm.reset();
        setTimeout(() => this.router.navigate(['/']), 2000);
      },
      error: err => {
        // Affiche le message d'erreur précis si dispo
        this.error = (err?.error?.detail || err?.error?.message || "Échec de la candidature");
        this.loading = false;
      }
    });
  }
}
