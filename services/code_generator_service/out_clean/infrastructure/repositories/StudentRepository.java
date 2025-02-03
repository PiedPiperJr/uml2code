package mwm.infrastructure.repositories;

import mwm.domain.entities.Student;
import mwm.domain.repositories.IStudentRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.UUID;
import java.util.List;

@Repository
public interface StudentJpaRepository extends JpaRepository<Student, UUID>, 
    IStudentRepository<Student, UUID> {
    
    
    
    
    
    
    
    
    
    
}