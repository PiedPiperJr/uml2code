// Service Implementation Template
package mwm.infrastructure.service.crud;

import mwm.domain.entities.Person;
import mwm.domain.service.crud.IPersonCrudService;
import mwm.infrastructure.repositories.PersonJpaRepository;
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
public class PersonService implements IPersonCrudService {
    
    private final PersonJpaRepository repository;
    
    @Override
    public Person create(Person entity) {
        return repository.save(entity);
    }
    
    @Override
    @Transactional(readOnly = true)
    public Person findById(UUID id) {
        return repository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("Person not found with id: " + id));
    }
    
    @Override
    @Transactional(readOnly = true)
    public Page<Person> findAll(Pageable pageable) {
        return repository.findAll(pageable);
    }
    
    @Override
    public Person update(UUID id, Person entity) {
        if (!repository.existsById(id)) {
            throw new EntityNotFoundException("Person not found with id: " + id);
        }
        entity.setId(id);
        return repository.save(entity);
    }
    
    @Override
    public void delete(UUID id) {
        if (!repository.existsById(id)) {
            throw new EntityNotFoundException("Person not found with id: " + id);
        }
        repository.deleteById(id);
    }
    
    
    
    
    
    
    
    
    
    
}