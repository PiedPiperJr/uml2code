// Service Interface Template
package mwm.domain.service.crud;

import mwm.domain.entities.Student;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import java.util.UUID;
import java.util.List;
import java.util.Optional;

public interface IStudentCrudService {
    Student create(Student entity);
    Student findById(UUID id);
    Page<Student> findAll(Pageable pageable);
    Student update(UUID id, Student entity);
    void delete(UUID id);
    
    
    
    
    
    
}