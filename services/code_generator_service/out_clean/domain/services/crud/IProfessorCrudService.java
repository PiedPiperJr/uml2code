// Service Interface Template
package mwm.domain.service.crud;

import mwm.domain.entities.Professor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import java.util.UUID;
import java.util.List;
import java.util.Optional;

public interface IProfessorCrudService {
    Professor create(Professor entity);
    Professor findById(UUID id);
    Page<Professor> findAll(Pageable pageable);
    Professor update(UUID id, Professor entity);
    void delete(UUID id);
    
    
    
    
    
    
    
    
    
    
}