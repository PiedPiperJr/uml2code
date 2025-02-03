// Service Implementation Template
package mwm.infrastructure.service.crud;

import mwm.domain.entities.Student;
import mwm.domain.service.crud.IStudentCrudService;
import mwm.infrastructure.repositories.StudentJpaRepository;
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
public class StudentService implements IStudentCrudService {
    
    private final StudentJpaRepository repository;
    
    @Override
    public Student create(Student entity) {
        return repository.save(entity);
    }
    
    @Override
    @Transactional(readOnly = true)
    public Student findById(UUID id) {
        return repository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("Student not found with id: " + id));
    }
    
    @Override
    @Transactional(readOnly = true)
    public Page<Student> findAll(Pageable pageable) {
        return repository.findAll(pageable);
    }
    
    @Override
    public Student update(UUID id, Student entity) {
        if (!repository.existsById(id)) {
            throw new EntityNotFoundException("Student not found with id: " + id);
        }
        entity.setId(id);
        return repository.save(entity);
    }
    
    @Override
    public void delete(UUID id) {
        if (!repository.existsById(id)) {
            throw new EntityNotFoundException("Student not found with id: " + id);
        }
        repository.deleteById(id);
    }
    
    
    
    
    
    
}