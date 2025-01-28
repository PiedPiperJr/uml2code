package org.enspy.4gi.domain.entities;

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
public class Address {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    
    
    @Column(nullable = true) // Add specific constraints if needed
    private str street;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private str city;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private str state;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private int postalcode;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private str country;
    
    

    // TODO: Add relationships here

    @CreationTimestamp
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;

}