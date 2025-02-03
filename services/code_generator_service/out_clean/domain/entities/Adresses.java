package mwm.domain.entities;


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
public class Adresses  {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    
    
    @Column(nullable = true) // Add specific constraints if needed
    private str city;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private str state;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private int postalCode;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private str country;
    
    

    // TODO: Add relationships here
    // Aggregation: List of related elements
    
    
    // Composition: List of owned elements
    

    @CreationTimestamp
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;

    // Methods
    
    private bool Validate() {
        // To implement
    }
    
    public str outputAsLabel() {
        // To implement
    }
    

}