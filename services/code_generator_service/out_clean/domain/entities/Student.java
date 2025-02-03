package mwm.domain.entities;

 
import mwm.domain.entities.Person; 

import lombok.*;
import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;
import java.time.LocalDateTime;
import java.util.*;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Student  extends Person  {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    
    
    @Column(nullable = true) // Add specific constraints if needed
    private int studentNumber;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private int averageMark;
    
    

    // TODO: Add relationships here
    // Aggregation: List of related elements
    
    
    // Composition: List of owned elements
    

    @CreationTimestamp
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;

    // Methods
    
    public bool isEligibleToEnroll() {
        // To implement
    }
    
    public int getSeminarsTaken(String papa) {
        // To implement
    }
    

}