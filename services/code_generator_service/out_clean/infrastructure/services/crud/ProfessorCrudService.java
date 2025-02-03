// Service Implementation Template
package mwm.infrastructure.service.crud;

import mwm.domain.entities.Professor;
import mwm.domain.service.crud.IProfessorCrudService;
import mwm.infrastructure.repositories.ProfessorJpaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import jakarta.persistence.EntityNotFoundException;
import java.util.UUID;
import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional
public class ProfessorService implements IProfessorCrudService {
    
    private final ProfessorJpaRepository repository;
    
    @Override
    public Professor create(Professor entity) {
        return repository.save(entity);
    }
    
    @Override
    @Transactional(readOnly = true)
    public Professor findById(UUID id) {
        return repository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("Professor not found with id: " + id));
    }
    
    @Override
    @Transactional(readOnly = true)
    public Page<Professor> findAll(Pageable pageable) {
        return repository.findAll(pageable);
    }
    
    @Override
    public Professor update(UUID id, Professor entity) {
        if (!repository.existsById(id)) {
            throw new EntityNotFoundException("Professor not found with id: " + id);
        }
        entity.setId(id);
        return repository.save(entity);
    }
    
    @Override
    public void delete(UUID id) {
        if (!repository.existsById(id)) {
            throw new EntityNotFoundException("Professor not found with id: " + id);
        }
        repository.deleteById(id);
    }
    
    
    
    
    
    
    
    
    
    
}