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
public class Person  {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    
    
    @Column(nullable = true) // Add specific constraints if needed
    private str name;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private str phoneNumber;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private str emailAddress;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private Address addresss;
    
    

    // TODO: Add relationships here
    // Aggregation: List of related elements
    
    
    // Composition: List of owned elements
    

    @CreationTimestamp
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;

    // Methods
    
    public void purchaseParkingPass() {
        // To implement
    }
    

}