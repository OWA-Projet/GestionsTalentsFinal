import { Routes } from '@angular/router';
import { AuthGuard } from './core/auth.guard';    // À créer (voir ci-dessous)
import { RoleGuard } from './core/role.guards';    // À créer

export const routes: Routes = [

  {
    path: 'contact', loadComponent: () =>
      import('./features/contact/contact.component').then(m => m.ContactComponent)
  },

  {
    path: 'about', loadComponent: () => 
          import('./features/about/about').then(m => m.About) 
  },
  { path: 'login', loadComponent: () => 
    import('./features/login.component/login.component').then(m => m.LoginComponent) 
  },
  {
    path: 'register', loadComponent: () => 
    import('./features/register/register.component').then(m => m.RegisterComponent) 
  },
  {
    path: '',
    loadComponent: () =>
      import('./features/acceuil.component/acceuil.component').then(m => m.AcceuilComponent)
  },
    {
            path: 'detail-offre/:id',
            data: { roles: ['RH'] },
            loadComponent: () => import('./features/offre-detail/offre-detail').then(m => m.OffreDetailComponent)
          },
          {
            path: 'offres-cv/:id/cvs',
            loadComponent: () =>
              import('./features/cv-offres/cv-offres.component').then(m => m.CvsOffreComponent),
            // canActivate: [RoleGuard], data: { roles: ['RH'] } // pour sécuriser
          },
          {
           path: 'cv-classes/:offreId',
           loadComponent: () =>
            import('./features/cv-classes/cv-classes.component').then(m => m.CvClassesComponent),
          },
            // ...
            { path: 'espace-candidat',
              loadComponent: () =>
                import('./features/espace-candidat/espace-candidat.component').then(m => m.EspaceCandidatComponent),
        
        },
        { path: 'qcm/:offreId',
          loadComponent: () =>
            import('./features/qcm/qcm.component').then(m => m.QcmComponent),
    
    },
    { path: 'profile',
          loadComponent: () =>
            import('./features/profile/profile.component').then(m => m.ProfilUtilisateurComponent),
    
    },

          
          
  // Contenus protégés
  {
    path: '',
    canActivate: [AuthGuard],
    children: [
      {
        path: 'user-list',
      loadComponent: () => import('./features/Utilisateur-list/utilisateur-list.component').then(m => m.UserListComponent)
      },
          {
      path: 'user-list',
      data: { roles: ['ADMIN'] },   // ← adapte les rôles selon ta logique
      loadComponent: () => import('./features/Utilisateur-list/utilisateur-list.component').then(m => m.UserListComponent)
    },
    {
      path: 'user-formulaire',
      data: { roles: ['ADMIN'] },
      loadComponent: () => import('./features/Utilisateur-form/utilisateur-form.component').then(m => m.UserFormulaireComponent)
    },
    {
      path: 'user-formulaire/:id',
      data: { roles: ['ADMIN'] },
      loadComponent: () => import('./features/Utilisateur-form/utilisateur-form.component').then(m => m.UserFormulaireComponent)
    },
          {
            path: 'postuler/:id',
            data: { roles: ['CANDIDAT'] },
            loadComponent: () => import('./features/postuler/postuler').then(m => m.PostulerComponent)
          },
          {
            path: 'offres-rh',
            data: { roles: ['RH'] },
            loadComponent: () => import('./features/offres-rh/offres-rh.component').then(m => m.OffresRhComponent)
          },
          {
            path: 'offres-formulaire/entreprise/:identreprise',
            data: { roles: ['RH'] },
            loadComponent: () => import('./features/offre-emploi-formulaire/offre-emploi-formulaire.component').then(m => m.OffreEmploiFormulaireComponent)
          },
          {
            path: 'offres-formulaire/:id',
            data: { roles: ['RH'] },
            loadComponent: () => import('./features/offre-emploi-formulaire/offre-emploi-formulaire.component').then(m => m.OffreEmploiFormulaireComponent)
          },

          {
            path: 'entreprise',
            data: { roles: ['ADMIN'] },
            loadComponent: () => import('./features/entreprise/entreprise.component').then(m => m.EntrepriseListComponent)
          },
          {
            path: 'entreprise-formulaire',
            loadComponent: () => import('./features/entreprise-formulaire/entreprise-formulaire.component').then(m => m.EntrepriseFormulaireComponent)
          },
          {
            path: 'entreprise-formulaire/:id',
            loadComponent: () => import('./features/entreprise-formulaire/entreprise-formulaire.component').then(m => m.EntrepriseFormulaireComponent)
          },
          {
            path: 'metier-list',
            data: { roles: ['RH'] },
            loadComponent: () => import('./features/metier-list/metier-list.component').then(m => m.MetierListComponent)
          },
          {
            path: 'metier-formulaire',
            loadComponent: () => import('./features/metier-form/metier-formulaire.component').then(m => m.MetierFormulaireComponent)
          },
          {
            path: 'metier-formulaire/:id',
            loadComponent: () => import('./features/metier-form/metier-formulaire.component').then(m => m.MetierFormulaireComponent)
          },

        ]
      }
      
    ,

  // Page 404
  {
    path: '**',
    loadComponent: () =>
      import('./features/page-not-found.component/page-not-found.component').then(m => m.PageNotFoundComponent)
  }
];
