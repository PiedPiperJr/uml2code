// Service Interface Template
package mwm.domain.service.crud;

import mwm.domain.entities.Person;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import java.util.UUID;
import java.util.List;
import java.util.Optional;

public interface IPersonCrudService {
    Person create(Person entity);
    Person findById(UUID id);
    Page<Person> findAll(Pageable pageable);
    Person update(UUID id, Person entity);
    void delete(UUID id);
    
    
    
    
    
    
    
    
    
    
}