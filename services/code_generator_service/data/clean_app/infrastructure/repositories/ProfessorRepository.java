package org.enspy.4gi.infrastructure.repositories;

import org.enspy.4gi.domain.entities.Professor;
import org.enspy.4gi.domain.repositories.IProfessorRepository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.*;

@Repository
public interface ProfessorJpaRepository extends JpaRepository< Professor, UUID>, IProfessorRepository< Professor, UUID>
{
    //TODO: Implement the repository logic here base on the AI
}