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
public class Person {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    
    
    @Column(nullable = true) // Add specific constraints if needed
    private str name;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private str phonenumber;
    
    
    
    @Column(nullable = true) // Add specific constraints if needed
    private str emailaddress;
    
    

    // TODO: Add relationships here

    @CreationTimestamp
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;

}