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
public class Professor  extends Person  {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    
    
    @Column(nullable = true) // Add specific constraints if needed
    private void name;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private int staffNumber;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private int yearsOfService;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private int numberOfClasses;
    
    

    // TODO: Add relationships here
    // Aggregation: List of related elements
    
    
    // Composition: List of owned elements
    
    private List<Adresses> adressess;
    

    @CreationTimestamp
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;

    // Methods
    

}